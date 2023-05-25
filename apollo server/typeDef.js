import { gql } from "apollo-server";

const typeDefs = gql`
    type Inputs {
        start_time: String!,
        end_time: String!,
        stock_symbol: ID!,
        model_type: String!,
        clear_type: String!,
    }
    type Query {
        inputs: [Inputs!]
    }
`;
export default typeDefs;