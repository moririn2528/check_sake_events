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
exports.searchPlaceFlow = void 0;
const z = __importStar(require("zod"));
const core_1 = require("@genkit-ai/core");
const flow_1 = require("@genkit-ai/flow");
const googleai_1 = require("@genkit-ai/googleai");
const core_2 = require("@genkit-ai/core");
const dotprompt_1 = require("@genkit-ai/dotprompt");
require("dotenv/config");
require("./schedule");
(0, core_1.configureGenkit)({
    plugins: [(0, dotprompt_1.dotprompt)(), (0, googleai_1.googleAI)()],
    logLevel: "debug",
    // Perform OpenTelemetry instrumentation and enable trace collection.
    enableTracingAndMetrics: true,
});
const prompt = (0, dotprompt_1.promptRef)("place");
const PlaceSchema = (0, core_2.defineSchema)("PlaceSchema", z.array(z.object({
    name: z.string(),
    address: z.ostring(),
})));
exports.searchPlaceFlow = (0, flow_1.defineFlow)({
    name: "searchPlaceFlow",
    inputSchema: z.string(),
    outputSchema: PlaceSchema,
}, async (body) => {
    // Construct a request and send it to the model API.
    const res = await prompt.generate({
        input: {
            body: body,
        },
    });
    const output = res.output();
    if (output === null) {
        return [];
    }
    return output;
});
(0, flow_1.startFlowsServer)();
// for cloud functions
// functions.http("completeEventInformation", (req, res) => {
//   res.send("Hello World!");
// });
//# sourceMappingURL=index.js.map