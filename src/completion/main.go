package main

import (
	"context"
	"errors"
	"fmt"
	"log"

	// Import the Genkit core libraries.
	"github.com/firebase/genkit/go/ai"
	"github.com/firebase/genkit/go/genkit"
	"github.com/joho/godotenv"

	// Import the Google AI plugin.
	"github.com/firebase/genkit/go/plugins/googleai"
)

func init() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}
}

func main() {
	ctx := context.Background()

	if err := googleai.Init(ctx, nil); err != nil {
		log.Fatal(err)
	}

	genkit.DefineFlow("menuSuggestionFlow", func(ctx context.Context, input string) (string, error) {
		m := googleai.Model("gemini-1.5-flash")
		if m == nil {
			return "", errors.New("menuSuggestionFlow: failed to find model")
		}

		resp, err := m.Generate(ctx,
			ai.NewGenerateRequest(
				&ai.GenerationCommonConfig{Temperature: 1},
				ai.NewUserTextMessage(fmt.Sprintf(`Suggest an item for the menu of a %s themed restaurant`, input))),
			nil)
		if err != nil {
			return "", err
		}

		text := resp.Text()
		return text, nil
	})

	if err := genkit.Init(ctx, nil); err != nil {
		log.Fatal(err)
	}
}
