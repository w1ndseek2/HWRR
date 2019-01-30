package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/sqlite"
	"io/ioutil"
	"os"
	"strconv"
	"sync"
)

type Pack struct {
	gorm.Model
	Datas []Data
}

type Image string
type Data struct {
	ID     uint
	PackID uint
	Img    Image
	Move   string
}
type Point struct {
	X    string `json:"x"`
	Y    string `json:"y"`
	Time string `json:"t"`
}
type Packs []Pack
type Datas []Data
type Points []Point

func main() {
	if len(os.Args) < 2 {
		panic("not specify database")
	}
	DataBase, err := gorm.Open("sqlite3", os.Args[1])
	if err != nil {
		panic(err)
	}
	defer DataBase.Close()
	var packs Packs
	a := DataBase.Find(&packs)
	if a.Error != nil {
		panic(a.Error)
	}
	var (
		wg   sync.WaitGroup
		lock sync.Mutex
	)
	file, _ := os.Create("data.txt")
	for _, v := range packs {
		wg.Add(1)
		go func(p Pack) {
			fmt.Printf("process pack[%d]\n", p.ID)
			var data Datas
			DataBase.Model(&p).Association("Datas").Find(&data)
			data.PictureGenerate("./pic")
			lock.Lock()
			data.DataGenerate(file)
			lock.Unlock()
			wg.Done()
		}(v)
	}
	wg.Wait()
}
func (d *Datas) PictureGenerate(rootPath string) {
	var ret bytes.Buffer
	ret.Write([]byte("<html><body>"))
	for _, v := range *d {
		ret.Write([]byte("<img src=\""))
		ret.WriteString(string(v.Img))
		ret.Write([]byte("\">"))
	}
	ret.Write([]byte("</body></html>"))
	fmt.Printf("generate picture[%d]\n", (*d)[0].PackID)
	err := ioutil.WriteFile(fmt.Sprintf("%s/%d.html", rootPath, (*d)[0].PackID), ret.Bytes(), 0644)
	if err != nil {
		panic(err)
	}
}
func (d *Datas) DataGenerate(f *os.File) {
	var (
		wg   sync.WaitGroup
		lock sync.Mutex
		file bytes.Buffer
	)
	for _, v := range *d {
		wg.Add(1)
		go func(data Data) {
			var (
				points   Points
				x        bytes.Buffer
				y        bytes.Buffer
				t        bytes.Buffer
				baseTime int
			)
			err := json.Unmarshal([]byte(v.Move), &points)
			if err != nil {
				panic(err)
			}
			for i, per := range points {
				x.WriteString(per.X)
				x.WriteByte(',')
				y.WriteString(per.Y)
				y.WriteByte(',')
				if i == 0 {
					baseTime, _ = strconv.Atoi(per.Time)
				}
				realTime, _ := strconv.Atoi(per.Time)
				realTime = realTime - baseTime
				t.WriteString(strconv.Itoa(realTime))
				t.WriteByte(',')
			}
			lock.Lock()
			file.Write(t.Bytes())
			file.WriteByte('\n')
			file.Write(x.Bytes())
			file.WriteByte('\n')
			file.Write(y.Bytes())
			file.WriteByte('\n')
			lock.Unlock()
			wg.Done()
		}(v)
	}
	wg.Wait()
	fmt.Printf("generate data[%d]\n", (*d)[0].PackID)
	_, err := f.Write(file.Bytes())
	if err != nil {
		panic(err)
	}
}
