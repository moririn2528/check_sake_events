import * as z from "zod";

import { configureGenkit } from "@genkit-ai/core";
import { defineFlow, startFlowsServer } from "@genkit-ai/flow";
import { googleAI } from "@genkit-ai/googleai";
import { defineSchema } from "@genkit-ai/core";
import { dotprompt, promptRef } from "@genkit-ai/dotprompt";
import "dotenv/config";
import functions from "@google-cloud/functions-framework";

import "./schedule";

configureGenkit({
  plugins: [dotprompt(), googleAI()],
  logLevel: "debug",
  // Perform OpenTelemetry instrumentation and enable trace collection.
  enableTracingAndMetrics: true,
});

const prompt = promptRef("place");
const PlaceSchema = defineSchema(
  "PlaceSchema",
  z.array(
    z.object({
      name: z.string(),
      address: z.ostring(),
    })
  )
);

export const searchPlaceFlow = defineFlow(
  {
    name: "searchPlaceFlow",
    inputSchema: z.string(),
    outputSchema: PlaceSchema,
  },
  async (body) => {
    // Construct a request and send it to the model API.
    const res = await prompt.generate<typeof PlaceSchema>({
      input: {
        body: body,
      },
    });
    const output = res.output();
    if (output === null) {
      return [];
    }
    return output;
  }
);

startFlowsServer();

// for cloud functions
// functions.http("completeEventInformation", (req, res) => {
//   res.send("Hello World!");
// });
