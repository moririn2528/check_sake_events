package utils

import (
	"archive/zip"
	"context"
	"io"
	"log"
	"os"
	"path/filepath"
	"strings"

	"cloud.google.com/go/storage"
)

type Storage struct {
	Bucket string
	File   string
}

func (s *Storage) createZip() {
	path, err := os.Getwd()
	if err != nil {
		log.Println(err)
		return
	}
	root := filepath.Join(path, "../scraper")

	zipFile, err := os.Create(s.File)
	if err != nil {
		log.Println(err)
		return
	}
	defer zipFile.Close()
	writer := zip.NewWriter(zipFile)
	defer writer.Close()

	err = filepath.Walk(root, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if info.IsDir() {
			return nil
		}

		relPath, err := filepath.Rel(root, path)
		if err != nil {
			return err
		}
		for _, dir := range strings.Split(relPath, "/") {
			if dir == "__pycache__" || dir == "credentials.json" || (filepath.Ext(dir) == ".env" && dir != ".env") {
				return nil
			}
		}

		w, err := writer.Create(relPath)
		if err != nil {
			return err
		}

		file, err := os.Open(path)
		if err != nil {
			return err
		}
		defer file.Close()

		_, err = io.Copy(w, file)
		if err != nil {
			return err
		}

		return nil
	})
	if err != nil {
		log.Println(err)
		return
	}
}

func (s *Storage) sendZip() {
	ctx := context.Background()

	client, err := storage.NewClient(ctx)
	if err != nil {
		log.Fatalf("Failed to create client: %v", err)
	}
	defer client.Close()
	bucket := client.Bucket(s.Bucket)
	obj := bucket.Object(s.File)
	w := obj.NewWriter(ctx)
	file, err := os.Open(s.File)
	if err != nil {
		log.Fatalf("Failed to open file: %v", err)
	}
	defer file.Close()
	if _, err := io.Copy(w, file); err != nil {
		log.Fatalf("Failed to write to bucket: %v", err)
	}
	if err := w.Close(); err != nil {
		log.Fatalf("Failed to close writer: %v", err)
	}
}

// ローカルフォルダを zip に圧縮し、Google Cloud Storage にアップロード
func (s *Storage) UploadFunction() {
	s.createZip()
	s.sendZip()
}
