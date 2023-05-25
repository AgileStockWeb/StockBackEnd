import Inputs from "./tempData.js";

const resolvers = {
  Query: {
    inputs: () => {
      return Inputs;
    },
  },
};

export default resolvers;