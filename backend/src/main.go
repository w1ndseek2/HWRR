package main

import (
	"encoding/json"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/jinzhu/gorm"
	"sync"
)

type Image string

type Point struct {
	X    string `json:"x" binding:"required"`
	Y    string `json:"y" binding:"required"`
	Time string `json:"t" binding:"required"`
}
type TouchList []Point
type PostData struct {
	Img        Image     `json:"img" binding:"required"`
	TouchStart Point     `json:"touchstart" binding:"required"`
	TouchMove  TouchList `json:"touchmove" binding:"required"`
}
type PostDataEx []PostData

var DataBase *gorm.DB

func main() {
	gin.SetMode(gin.ReleaseMode)
	router := gin.Default()
	router.POST("/api/submit", func(context *gin.Context) {
		var data PostDataEx
		if err := context.ShouldBindJSON(&data); err == nil {
			HandleData(&data)
			context.JSON(200, nil)
		} else {
			fmt.Println(err)
			context.JSON(400, nil)
		}
	})
	_ = router.Run()
}

func HandleData(d *PostDataEx) {
	var newDataArr []Data
	var lock sync.Mutex
	var wg sync.WaitGroup
	for _, v := range *d {
		wg.Add(1)
		go func(data PostData) {
			move, _ := json.Marshal(data.TouchMove)
			newData := Data{
				Img:  data.Img,
				Move: string(move),
			}
			lock.Lock()
			newDataArr = append(newDataArr, newData)
			lock.Unlock()
			wg.Done()
		}(v)
	}
	wg.Wait()
	var newPack Pack
	DataBase.Create(&newPack)
	DataBase.Model(&newPack).Association("Datas").Append(newDataArr)
}
