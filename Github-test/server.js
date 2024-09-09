// server.js
const express = require('express');
const { graphqlHTTP } = require('express-graphql');
const { buildSchema } = require('graphql');

// Sample schema and data
const schema = buildSchema(`
  type Query {
    user(id: ID!): User
  }

  type User {
    id: ID
    name: String
    age: Int
  }
`);

// Sample data
const users = {
    1: { id: 1, name: 'John Doe', age: 30 },
    2: { id: 2, name: 'Jane Smith', age: 25 }
};

// Root resolver
const root = {
    user: ({ id }) => users[id],
};

// Initialize Express app
const app = express();

// Define GraphQL endpoint
app.use('/graphql', graphqlHTTP({
    schema: schema,
    rootValue: root,
    graphiql: true,  // Enable GraphiQL for manual testing
}));

// Start the server
app.listen(4000, () => {
    console.log('Running a GraphQL API server at http://localhost:4000/graphql');
});
