package main

import (
	"fmt"
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/sqlite"
	"os"
)

var DataBaseName = "data.db"

type Pack struct {
	gorm.Model
	Datas []Data
}
type Data struct {
	ID     uint `gorm:"AUTO_INCREMENT;primary_key"`
	PackID uint
	Img    Image  `gorm:"size:2147483647"`
	Move   string `gorm:"size:2147483647"`
}

func init() {
	//fmt.Println("data.init()")
	//defer func() { fmt.Println("defer data.init()") }()
	db, err := gorm.Open("sqlite3", DataBaseName)
	if err != nil {
		_, _ = os.Create(DataBaseName)
		db, err = gorm.Open("sqlite3", DataBaseName)
		if err != nil {
			fmt.Println(err)
			panic("open and create error")
		}
	}
	dataTable := db.HasTable(&Data{})
	packTable := db.HasTable(&Pack{})
	if !dataTable || !packTable {
		if dataTable {
			db.DropTable(&Data{})
		}
		if packTable {
			db.DropTable(&Pack{})
		}
		db.CreateTable(&Data{})
		db.CreateTable(&Pack{})
	}
	DataBase = db
}
