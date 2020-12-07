package main

import (
	"fmt"
	"io/ioutil"
	"log"

	"net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "%s", r.Header.Get("x-request-id"))

	fmt.Fprintf(w, "Service D Calling Service B ")

	req, err := http.NewRequest("GET", "http://service_d_envoy:8788/request2", nil)
	if err != nil {
		fmt.Printf("%s", err)
	}

	req.Header.Add("x-request-id", r.Header.Get("x-request-id"))
	req.Header.Add("x-b3-traceid", r.Header.Get("x-b3-traceid"))
	req.Header.Add("x-b3-spanid", r.Header.Get("x-b3-spanid"))
	req.Header.Add("x-b3-parentspanid", r.Header.Get("x-b3-parentspanid"))
	req.Header.Add("x-b3-sampled", r.Header.Get("x-b3-sampled"))
	req.Header.Add("x-b3-flags", r.Header.Get("x-b3-flags"))
	req.Header.Add("x-ot-span-context", r.Header.Get("x-ot-span-context"))

	client := &http.Client{}
	resp, err := client.Do(req)

	if err != nil {
		fmt.Printf("%s", err)
	}

	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("%s", err)
	}
	fmt.Fprintf(w, string(body))
	fmt.Fprintf(w, "Hello from service D ")

	sum := 5.2
	for i := 1; i < 1000; i++ {
		for j := 1; j < 100; j++ {
			sum *= float64((i + j))
		}
	}

	// req, err = http.NewRequest("GET", "http://service_d_envoy:8791/", nil)
	// if err != nil {
	// 	fmt.Printf("%s", err)
	// }

	// // req.Header.Add("x-request-id", r.Header.Get("x-request-id"))
	// // req.Header.Add("x-b3-traceid", r.Header.Get("x-b3-traceid"))
	// // req.Header.Add("x-b3-spanid", r.Header.Get("x-b3-spanid"))
	// // req.Header.Add("x-b3-parentspanid", r.Header.Get("x-b3-parentspanid"))
	// // req.Header.Add("x-b3-sampled", r.Header.Get("x-b3-sampled"))
	// // req.Header.Add("x-b3-flags", r.Header.Get("x-b3-flags"))
	// // req.Header.Add("x-ot-span-context", r.Header.Get("x-ot-span-context"))

	// client = &http.Client{}
	// resp, err = client.Do(req)

	// if err != nil {
	// 	fmt.Printf("%s", err)
	// }

	// defer resp.Body.Close()
	// body, err = ioutil.ReadAll(resp.Body)
	// if err != nil {
	// 	fmt.Printf("%s", err)
	// }

	// fmt.Fprintf(w, string(body))
}

func main() {

	http.HandleFunc("/", handler)
	log.Fatal(http.ListenAndServe(":8086", nil))
}
