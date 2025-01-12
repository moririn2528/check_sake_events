import * as z from "zod";

import { defineFlow } from "@genkit-ai/flow";
import { defineSchema } from "@genkit-ai/core";
import { promptRef } from "@genkit-ai/dotprompt";
import "dotenv/config";

const prompt = promptRef("schedule");
const InputScheduleSchema = defineSchema(
  "InputScheduleSchema",
  z.object({
    body: z.string(),
    place: z.string(),
  })
);
const OutputScheduleSchema = defineSchema(
  "OutputScheduleSchema",
  z.object({
    period: z.object({
      start: z.optional(
        z.date().describe("default timezone is Japanese time zone")
      ),
      end: z.optional(
        z.date().describe("default timezone is Japanese time zone")
      ),
    }),
    cost: z.ostring(),
  })
);

export const searchScheduleFlow = defineFlow(
  {
    name: "searchScheduleFlow",
    inputSchema: InputScheduleSchema,
    outputSchema: OutputScheduleSchema,
  },
  async ({ body, place }) => {
    // Construct a request and send it to the model API.
    const res = await prompt.generate<typeof OutputScheduleSchema>({
      input: {
        body,
        place,
      },
    });
    const output = res.output();
    if (output === null) {
      return {
        period: {
          start: undefined,
          end: undefined,
        },
        cost: "0",
      };
    }
    return output;
  }
);
