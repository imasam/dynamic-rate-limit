package main

import (
	"fmt"
	"log"

	"net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
	sum := 3.2
	for i := 1; i < 100; i++ {
		for j := 1; j < 500; j++ {
			sum *= float64((i + j))
		}
	}
	fmt.Fprintf(w, "Hello from service C ")
}

func main() {
	http.HandleFunc("/", handler)
	log.Fatal(http.ListenAndServe(":8083", nil))
}
