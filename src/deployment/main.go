package main

import (
	"context"
	"os"

	"github.com/joho/godotenv"
	"sake-event.deployment.com/utils"
)

func main() {
	godotenv.Load()
	ctx := context.Background()

	projectID := os.Getenv("PROJECT_ID")
	region := "asia-northeast1"
	functionID := "crawlSakeEvents"
	bucketName := os.Getenv("BUCKET_NAME")
	sourceName := "function-source.zip"

	// ローカルファイルを GCS にアップロード
	storage := utils.Storage{
		Bucket: bucketName,
		File:   sourceName,
	}
	storage.UploadFunction()

	// Cloud Function をデプロイ
	function := utils.NewFunction(ctx, projectID, region, functionID, bucketName, sourceName)
	defer function.Close()
	function.Deploy()

}
