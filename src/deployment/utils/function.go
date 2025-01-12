package utils

import (
	"context"
	"fmt"
	"log"

	functions "cloud.google.com/go/functions/apiv2"
	"cloud.google.com/go/functions/apiv2/functionspb"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

type Function struct {
	projectID      string
	functionID     string
	resource       string
	parentResource string
	bucketName     string
	sourceName     string
	client         *functions.FunctionClient
}

func NewFunction(ctx context.Context, projectID, region, functionID, bucketName, sourceName string) *Function {
	client, err := functions.NewFunctionClient(ctx)
	if err != nil {
		log.Fatalf("Failed to create Cloud Functions client: %v", err)
	}
	return &Function{
		projectID:      projectID,
		functionID:     functionID,
		resource:       fmt.Sprintf("projects/%s/locations/%s/functions/%s", projectID, region, functionID),
		parentResource: fmt.Sprintf("projects/%s/locations/%s", projectID, region),
		bucketName:     bucketName,
		sourceName:     sourceName,
		client:         client,
	}
}

func (f *Function) Close() {
	f.client.Close()
}

func (f *Function) Deploy() {
	ctx := context.Background()

	// Cloud Function があれば更新、なければ作成
	log.Println("Deploying function...")
	function := &functionspb.Function{
		Name:        f.resource,
		Description: "crawling sake events",
		BuildConfig: &functionspb.BuildConfig{
			Runtime: "python312",
			Source: &functionspb.Source{
				Source: &functionspb.Source_StorageSource{
					StorageSource: &functionspb.StorageSource{
						Bucket: f.bucketName,
						Object: f.sourceName,
					},
				},
			},
		},
		ServiceConfig: &functionspb.ServiceConfig{
			AvailableMemory: "512M",
			TimeoutSeconds:  120,
		},
	}
	_, err := f.client.GetFunction(ctx, &functionspb.GetFunctionRequest{Name: f.resource})
	if status.Code(err) == codes.NotFound {
		op, err := f.client.CreateFunction(ctx, &functionspb.CreateFunctionRequest{
			Parent:     f.parentResource,
			Function:   function,
			FunctionId: f.functionID,
		})
		if err != nil {
			log.Fatalf("Failed to create function: %v", err)
		}
		_, err = op.Wait(ctx)
		if err != nil {
			log.Fatalf("Failed to update function operation: %v", err)
		}
	} else if err == nil {
		op, err := f.client.UpdateFunction(ctx, &functionspb.UpdateFunctionRequest{
			Function: function,
		})
		if err != nil {
			log.Fatalf("Failed to update function: %v", err)
		}
		_, err = op.Wait(ctx)
		if err != nil {
			log.Fatalf("Failed to update function operation: %v", err)
		}
	} else {
		log.Fatalf("Failed to get function: %v", err)
	}
}

func (f *Function) GetServiceAccountEmail() string {
	ctx := context.Background()

	// サービスアカウント取得
	funClient, err := functions.NewFunctionClient(ctx)
	if err != nil {
		log.Fatalf("Failed to create Cloud Functions client: %v", err)
	}
	defer funClient.Close()
	fun, err := f.client.GetFunction(ctx, &functionspb.GetFunctionRequest{Name: f.resource})
	if err != nil {
		log.Fatalf("Failed to get function: %v", err)
	}
	return fun.ServiceConfig.ServiceAccountEmail
}
