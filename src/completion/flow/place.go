package flow

import (
	"context"
	"errors"
	"log"

	"github.com/firebase/genkit/go/ai"
	"github.com/firebase/genkit/go/genkit"
	"github.com/firebase/genkit/go/plugins/googleai"
)

// Ex: https://pkg.go.dev/github.com/invopop/jsonschema@v0.12.0#example-Reflect
type Place struct {
	Name    string `json:"name" jsonschema:"title=開催場所"`
	Address string `json:"address,omitempty"`
}

func ExtractPlaces(body string) []Place {
	ctx := context.Background()
	f := genkit.DefineFlow("extractPlacesFlow", func(ctx context.Context, input string) ([]Place, error) {
		model := googleai.Model(MODEL_NAME)
		if model == nil {
			return nil, errors.New("extractPlacesFlow: failed to find model")
		}
		res, err := ai.Generate(ctx, model,
			ai.WithConfig(&ai.GenerationCommonConfig{Temperature: 0}),
			ai.WithMessages(
				ai.NewSystemTextMessage("日本酒に関するイベント情報が与えられます。このイベントの開催場所を教えてください。住所も書かれている場合はそれも教えてください。開催場所が複数ある場合はすべて答えてください。記載されていない場合は答えないでください。"),
				ai.NewUserMessage(ai.NewDataPart(body)),
			),
			ai.WithOutputSchema([]Place{}),
		)
		if err != nil {
			return nil, err
		}
		var places []Place
		err = res.UnmarshalOutput(&places)
		if err != nil {
			return nil, err
		}
		return places, nil
	})
	places, err := f.Run(ctx, body)
	if err != nil {
		log.Fatalln(err)
	}
	return places
}

// configureGenkit({
//   plugins: [dotprompt(), googleAI()],
//   logLevel: "debug",
//   // Perform OpenTelemetry instrumentation and enable trace collection.
//   enableTracingAndMetrics: true,
// });

// const prompt = promptRef("place");
// const PlaceSchema = defineSchema(
//   "PlaceSchema",
//   z.array(
//     z.object({
//       name: z.string(),
//       address: z.ostring(),
//     })
//   )
// );

// export const searchPlaceFlow = defineFlow(
//   {
//     name: "searchPlaceFlow",
//     inputSchema: z.string(),
//     outputSchema: PlaceSchema,
//   },
//   async (body) => {
//     // Construct a request and send it to the model API.
//     const res = await prompt.generate<typeof PlaceSchema>({
//       input: {
//         body: body,
//       },
//     });
//     const output = res.output();
//     if (output === null) {
//       return [];
//     }
//     return output;
//   }
// );
