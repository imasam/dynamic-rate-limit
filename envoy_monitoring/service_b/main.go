package main

import (
	"fmt"
	"log"

	"net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
	sum := 1.2
	for i := 1; i < 100; i++ {
		for j := 1; j < 100; j++ {
			sum *= float64((i + j))
		}
	}
	fmt.Fprintf(w, "Hello from service B ")
}

func main() {
	http.HandleFunc("/", handler)
	log.Fatal(http.ListenAndServe(":8082", nil))
}
