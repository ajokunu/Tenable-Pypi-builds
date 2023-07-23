package main

import ( 
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	
)
//this is the structure that must be built out to match the json being parsed
type post struct {
	Id int				`json:"id"`
	Content string		`json:"content"`
	Author Author		`json:"author"`
	Comments []Comment	`json:"comment"`
}
type author struct {
	Id int
	Name string
}

type comment struct {
	id int
	Content string
	author string
}

func main() {
	jsonFile, err := os.Open("post.json")
	if err != nil {
		fmt.Println("Error opening JSON file: ", err)
		return
	}

	defer jsonFile.Close()
	jsonData, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		fmt.Println("cannot read JSON file:", err)
		return
	}
	//breaks JSON into the struct etc
	var post Post
	json.unmarshal (jsonData, &post)
	fmt.Println(post)
}