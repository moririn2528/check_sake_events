"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.searchScheduleFlow = void 0;
const z = __importStar(require("zod"));
const flow_1 = require("@genkit-ai/flow");
const core_1 = require("@genkit-ai/core");
const dotprompt_1 = require("@genkit-ai/dotprompt");
require("dotenv/config");
const prompt = (0, dotprompt_1.promptRef)("schedule");
const InputScheduleSchema = (0, core_1.defineSchema)("InputScheduleSchema", z.object({
    body: z.string(),
    place: z.string(),
}));
const OutputScheduleSchema = (0, core_1.defineSchema)("OutputScheduleSchema", z.object({
    period: z.object({
        start: z.optional(z.date().describe("default timezone is Japanese time zone")),
        end: z.optional(z.date().describe("default timezone is Japanese time zone")),
    }),
    cost: z.ostring(),
}));
exports.searchScheduleFlow = (0, flow_1.defineFlow)({
    name: "searchScheduleFlow",
    inputSchema: InputScheduleSchema,
    outputSchema: OutputScheduleSchema,
}, async ({ body, place }) => {
    // Construct a request and send it to the model API.
    const res = await prompt.generate({
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
});
//# sourceMappingURL=schedule.js.map