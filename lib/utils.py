"""Helper parts for graphql-cop."""
import requests
from simplejson import JSONDecodeError
from version import VERSION
from datetime import datetime
import base64

requests.packages.urllib3.disable_warnings()

def curlify(obj):
  req = obj.request
  command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
  method = req.method
  uri = req.url
  if req.body:
    try:
      data = req.body.decode('UTF-8')
    except:
      reqb = bytes(req.body, 'UTF-8')
      data = reqb.decode('UTF-8')
  else:
    data = ''
  headers = ['"{0}: {1}"'.format(k, v) for k, v in req.headers.items()]
  headers = " -H ".join(headers)
  return command.format(method=method, headers=headers, data=data, uri=uri)

def get_error(resp):
  """Collect the error."""
  error = None
  try:
      error = resp['errors'][0]['message']
  except:
      pass
  return error

def graph_query(url, proxies, headers, operation='query', payload={}, batch=False):
  """Perform a query."""
  if batch:
    data = []
    for _ in range(10):
      data.append({operation:payload})
  else:
    data = {operation:payload, "operationName":"cop"}
  try:
    response = requests.post(url,
                            headers=headers,
                            cookies=None,
                            verify=False,
                            allow_redirects=True,
                            timeout=60,
                            proxies=proxies,
                            json=data)
    return response
  except Exception:
    return {}


def request(url, proxies, headers, params=None, data=None, verb='GET'):
  """Perform requests."""
  try:
    response = requests.request(verb,
                            url=url,
                            params=params,
                            headers=headers,
                            cookies=None,
                            verify=False,
                            allow_redirects=True,
                            proxies=proxies,
                            timeout=20,
                            data=data)
    return response
  except:
    return None



def is_graphql(url, proxies, headers, debug_mode):
  """Check if the URL provides a GraphQL interface."""
  if debug_mode:
    headers['X-GraphQL-Cop-Test'] = 'Looking for GraphQL Interface'
  query = '''
    query cop {
      __typename
    }
  '''
  response = graph_query(url, proxies, headers, payload=query)

  try:
    response.json()
  except AttributeError:
    return False
  except JSONDecodeError:
    return False

  if 'data' in response.json() and response.json()['data'] != None:
    if response.json()['data']['__typename'] in ('Query', 'QueryRoot', 'query_root', 'Root'):
      return True
  elif response.json().get('errors') and (any('locations' in i for i in response.json()['errors']) or (any('extensions' in i for i in response.json()))):
    return True
  elif response.json().get('data'):
    return True
  else:
    return False

def draw_art():
  """Create banner."""
  return '''
                GraphQL Cop {version}
           Security Auditor for GraphQL
             Dolev Farhi & Nick Aleks
  '''.format(version=VERSION)

def getBase64FromImage(path:str):
  with open(path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
  return encoded_string.decode()

def generate_html_output(path:str, json_output:list, urls:list):
  date = datetime.today().strftime('%d.%m.%Y')
  #create default name
  name = "GraphQL_security_audit_" + date.replace(".", "_") + ".html"
  if path.endswith(".html"): #if name exist try to assign it
    name = path.split("/")[-1]

  ScopeHtml = "<ul>"
  for u in urls:
    ScopeHtml += f"<li> {u} </li>"
  ScopeHtml += "</ul>"  
  
  severity_order = {
    "CRITICAL": 1,
    "HIGH": 2,
    "MEDIUM": 3,
    "LOW": 4,
    "INFO": 5
  }

  # Function to get the order value for sorting
  def get_severity_order(item):
    return severity_order.get(item["severity"], float('inf'))
  
  severity_dict = {"CRITICAL" : 0, "HIGH":0, "MEDIUM" :0, "LOW":0, "INFO":0}
  all = 0
  html_vulns_desc = ""
  sorted_json_output = sorted(json_output, key=get_severity_order)
  for vuln in sorted_json_output:
    if(vuln["result"] == True):
      color_scheme = ""
      if (vuln["severity"] == "CRITICAL"):
        color_scheme = "color:white;background-color:black"
      elif (vuln["severity"] == "HIGH"):
        color_scheme = "color:white;background-color:red"
      elif (vuln["severity"] == "MEDIUM"):
        color_scheme = "color:black;background-color:orange"
      elif (vuln["severity"] == "LOW"):
        color_scheme = "color:black;background-color:yellow"
      elif (vuln["severity"] == "INFO"):
        color_scheme = "color:black;background-color:lightgray"
      
      
      severity_dict[vuln["severity"]] += 1
      all +=1
      html_vulns_desc += f'''
      <hr>
      <h2> <span style={color_scheme}>  &nbsp;{vuln["severity"]} </span> &nbsp;  {vuln["title"]} </h2>
      <h3> {vuln["impact"]} </h3>
      <hr>
      <h4> Description  </h4>
      <p> {vuln["description"]}  </p>
      
      <h4> Proof in curl </h4>
      {
          ''' 
            <div class="code-container">
              <button class="copy-button">
                <span class="clipboard-icon">&#128203;</span>
                <span class="checkmark-icon">&#9989;</span>
              </button>
              <pre><code>
                
              
          ''' + vuln["curl_verify"]
          if(len(vuln["curl_verify"]) >= 2) else 
          ''' 
          <pre><code>
            Sorry, We couldn't generate curl proof for this vulnerability.
          '''
      }
        </code></pre>
      </div>
      <br>
      <br>  
      '''
  # calculate % for graph
  temp_severity_list = [0,0,0,0,0]
  if all != 0:
    last_not_zero_index=0
    for index,key in enumerate(severity_dict):
      percent = int(severity_dict[key]*100 / all)
      if percent != 0:
        last_not_zero_index = index

      temp_severity_list[index]=percent

    Sum = sum(temp_severity_list)
    if Sum > 100:
      temp_severity_list[last_not_zero_index] -=  (Sum-100)
    elif Sum < 100:
      temp_severity_list[last_not_zero_index] +=  (Sum-100)
      
  basic_html = f'''
  <html>
    <head>
        <!DOCTYPE html>
        <meta charset="UTF-8"> 
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin-left:30px">
      <center>
        <h1> Security audit for GraphQL </h1>
        <h2> {date} </h2>
        <img style='display: block;margin-left: auto;margin-right: auto;width: 30%;' src='data:image/png;base64, {getBase64FromImage("./static/images/logo.png")}' >
      </center>
      <br><hr>

      <div style="display:flex">
        <div style="flex: 0 0 55%;">
          <h2 style="position: absolute;left: 17%;transform: translate(0, -50%);"> Scope of the test </h2>
          <br><br>
          {ScopeHtml}
        </div>
        <div style="flex: 0 0 60%;display: flex;position: relative;margin-left:100px">
          <h2 style="position: absolute;left: 30%;transform: translate(-50%, -50%);"> Identified vulnerabilities </h2>
          <div style="flex: 1; margin-top:50px; margin-left:30px; margin-bottom:30px">
            <div class="pie"></div>
          </div>
          <div style="flex: 0 0 80%;padding:40px; margin-top:30px">
            <div class='row' style="margin-top:5px"><div class='box Critical'></div> <div style="white-space: pre;"> Critical   {severity_dict["CRITICAL"]}</div> </div>
            <div class='row' style="margin-top:5px" ><div class='box High'></div>     <div style="white-space: pre;"> High       {severity_dict["HIGH"]}</div></div>
            <div class='row' style="margin-top:5px" ><div class='box Medium'></div>   <div style="white-space: pre;"> Medium  {severity_dict["MEDIUM"]}</div></div>
            <div class='row' style="margin-top:5px" ><div class='box Low'></div>      <div style="white-space: pre;"> Low        {severity_dict["LOW"]}</div></div>
            <div class='row' style="margin-top:5px" ><div class='box Info'></div>     <div style="white-space: pre;"> Info        {severity_dict["INFO"]}</div></div>
          </div>
        </div>  
      </div>
      {html_vulns_desc}
  
    <style>
      h1, h2, h3, h4, h5, h6 {{
          font-size: 1.3em; 
      }}
      
      img{{
        max-height:500px;
        max-width:500px;
        height:auto;
        width:auto;
      }}

      .pie {{
      --slice1: {temp_severity_list[0]};  /* Percentage of the first slice */
      --slice2:  {temp_severity_list[1]};  /* Percentage of the second slice */
      --slice3:  {temp_severity_list[2]};  /* Percentage of the third slice */
      --slice4:  {temp_severity_list[3]};  /* Percentage of the fourth slice */
      --slice5:  {temp_severity_list[4]};  /* Percentage of the fifth slice */

      
      height: 200px;
      width: 200px;
      border-radius: 50%;
      background: conic-gradient(
        var(--color1) 0 calc(var(--slice1) * 1%),
        var(--color2) calc(var(--slice1) * 1%) calc((var(--slice1) + var(--slice2)) * 1%),
        var(--color3) calc((var(--slice1) + var(--slice2)) * 1%) calc((var(--slice1) + var(--slice2) + var(--slice3)) * 1%),
        var(--color4) calc((var(--slice1) + var(--slice2) + var(--slice3)) * 1%) calc((var(--slice1) + var(--slice2) + var(--slice3) + var(--slice4)) * 1%),
        var(--color5) calc((var(--slice1) + var(--slice2) + var(--slice3) + var(--slice4)) * 1%) 100%
      );

      /* Color Variables */
      --color1: black;
      --color2: red;
      --color3: orange;
      --color4: yellow;
      --color5: lightgray;
      
      position: relative; /* Necessary for absolute positioning */
      &::after {{
        content: "";
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 50%; /* Adjust the size as needed */
        height: 50%;
        background-color: white;
        border-radius: 50%;
      }}

    }}

      pre {{
        font-family: 'Courier New', Courier, monospace;
        background-color: #f5f5f5; 
        padding: 10px; 
        border-radius: 5px; 
        color: #333; 
        display: block; 
        white-space: normal;
        line-height: 1.5; 
        margin: 0 20px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); 
        padding-right: 40px;
      }}
      
      .code-container {{
            position: relative;
        }}

        .copy-button {{
            position: absolute;
            top: 5px;
            right: 5px;
            padding: 5px;
            background-color: transparent;
            border: none;
            cursor: pointer;
            font-size: 18px;
        }}

        .clipboard-icon {{
            position: absolute;
            right: 25px;
            font-size: 28px;
        }}

        
        .checkmark-icon {{
            position: absolute;
            right: 25px;
            font-size: 28px; 
            opacity: 0;
            transition: opacity 0.3s ease-in-out;
        }}
 
        .copy-button.copied .checkmark-icon {{
            animation: showCheckmark 2s ease-in-out;
        }}

        @keyframes showCheckmark {{
            0% {{
                opacity: 0;
            }}
            10% {{
                opacity: 0.7;
            }}
            70% {{
                opacity: 0.7;
            }}
            100% {{
                opacity: 0;
            }}
        }}

      .box {{
        float: left;
        height: 20px;
        width: 20px;
        border: 1px solid black;
        clear: both;
      }}
      .row {{
          display : flex;
          align-items : center;
          margin-left: 20px;
      }}

      .Critical {{
        background-color: black;
      }}
      .High {{
        background-color: red;
      }}

      .Medium {{
        background-color: orange;
      }}
      .Low {{
        background-color: yellow;
      }}
      .Info{{
        background-color: LightGray;
      }}
      @media print {{
        * {{
          -webkit-print-color-adjust: exact !important;   /* Chrome, Safari 6 – 15.3, Edge */
          color-adjust: exact !important;                 /* Firefox 48 – 96 */
          print-color-adjust: exact !important;           /* Firefox 97+, Safari 15.4+ */
        }}
        body {{
          overflow-x: hidden; 
          overflow-y: hidden; 
        }}
        @page {{
          header: none;
        }}
        
        .pie, span {{
          color: inherit; /* Inherit color from parent or default */
          background-color: inherit; /* Inherit background color */
        }}
        
        .Critical, .High, .Medium, .Low, .Info {{
          color: inherit; /* Inherit color from parent or default */
        }}
        .box{{
          border: 2px solid black !important;
          float: left;
          height: 20px;
          width: 20px;
        }}
        
        .clipboard-icon{{
          visibility: hidden;
        }}
        
        hr {{
          display: block;
          height: 1px;
          background: transparent;
          width: 100%;
          border: none;
          border-top: solid 3px #aaa;
        }}
        
        
      }}
    </style>
    
    <script>
      document.querySelectorAll('.copy-button').forEach(button => {{
        button.addEventListener('click', () => {{
            const codeBlock = button.nextElementSibling.querySelector('code');
            const range = document.createRange();
            range.selectNodeContents(codeBlock);
            const selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(range);

            try {{
                document.execCommand('copy');
                selection.removeAllRanges();
                button.classList.add('copied');
                setTimeout(() => {{
                  button.classList.remove('copied');
                }}, 2000);
            }} catch (err) {{
                console.error('Failed to copy text: ', err);
            }}
        }});
      }});
    </script>
    
  </body>
</html>
  '''
  
  with open(name, "w") as f: 
    f.write(basic_html)
  
  