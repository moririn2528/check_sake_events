package utils

// import (
// 	"context"
// 	"fmt"
// 	"log"

// 	admin "cloud.google.com/go/iam/admin/apiv1"
// 	"cloud.google.com/go/iam/apiv1/iampb"
// )

// type Firestore struct {
// 	projectID string
// }

// func NewFirestore(projectID string) *Firestore {
// 	return &Firestore{
// 		projectID: projectID,
// 	}
// }

// func (f *Firestore) SetAccessIAM(serviceAccountEmail string) {
// 	ctx := context.Background()

// 	role := "roles/datastore.user"
// 	member := fmt.Sprintf("serviceAccount:%s", serviceAccountEmail)
// 	client, err := admin.NewIamClient(ctx)
// 	if err != nil {
// 		log.Fatalf("Failed to create IAM client: %v", err)
// 	}
// 	defer client.Close()
// 	serviceAccount := fmt.Sprintf("projects/%s/serviceAccounts/%s", f.projectID, serviceAccountEmail)
// 	policy, err := client.GetIamPolicy(ctx, &iampb.GetIamPolicyRequest{
// 		Resource: serviceAccount,
// 	})
// 	if err != nil {
// 		log.Fatalf("Failed to get IAM policy: %v", err)
// 	}
// 	addPolicy(policy, role, member)

// 	// 権限更新
// 	_, err = client.SetIamPolicy(ctx, &admin.SetIamPolicyRequest{
// 		Resource: serviceAccount,
// 		Policy:   policy,
// 	})
// 	if err != nil {
// 		log.Fatalf("Failed to set IAM policy: %v", err)
// 	}
// }
