import { Component, OnInit } from '@angular/core';
import { ServiceService } from 'src/app/service.service';
import { DataService } from 'src/app/data.service';
import { HttpClient } from '@angular/common/http';
import {Sort} from '@angular/material/sort';
import { MatTableModule } from '@angular/material/table';


export interface Forex {
  buy_card: number;
  buy_cash: number;
  lastupdated: string;
  name: string;
  sell_card: number;
  sell_cash: number;
  site: string
}
export interface Currencies{
  value:string,
  viewValue:string
}

@Component({
  selector: 'app-forex',
  templateUrl: './forex.component.html',
  styleUrls: ['./forex.component.css']
})
export class ForexComponent implements OnInit {

  constructor(private service:ServiceService,  private dataservice: DataService , private http:HttpClient) { }

  listData = [];
  displayedColoums : string[] = ['buy_card','buy_cash', 'lastupdated', 'name', 'sell_card', 'sell_cash','site'];

  visible: boolean = false;

  forex: Forex[] = [];

  sortedData: Forex[] = [];


  source: string = "";
  target: string = "";
  source_currencies: Currencies[] = [
    {value: 'inr', viewValue: 'Indian Rupee'},
    {value: 'usd', viewValue: 'U.S. Dollar'},
    {value: 'gbp', viewValue: 'G.B. Pound'},
    {value: 'eur', viewValue: 'Euro'},
    {value: 'aud', viewValue: 'Australian Dollar'}
  ];

  
  forexProvider:any = []
  forexValues:any = []

  ngOnInit(): void {
    this.showAllData();
   }

   sortData(sort: Sort) {
     console.log("in sorted data")
    const data = this.forex.slice();
    if (!sort.active || sort.direction === '') {
      this.sortedData = data;
      return;
    }

    this.sortedData = data.sort((a, b) => {
      const isAsc = sort.direction === 'asc';
      switch (sort.active) {
        case 'name': return compare(a.name, b.name, isAsc);
        case 'buy_card': return compare(a.buy_card, b.buy_card, isAsc);
        case 'buy_cash': return compare(a.buy_cash, b.buy_cash, isAsc);
        case 'sell_cash': return compare(a.sell_cash, b.sell_cash, isAsc);
        case 'sell_card': return compare(a.sell_card, b.sell_card, isAsc);
        case 'site': return compare(a.site, b.site, isAsc);
        case 'lastupdated': return compare(a.lastupdated, b.lastupdated, isAsc);
        default: return 0;
      }
    });
  }

   selected(){
     console.log(this.source);
     console.log(this.target);
     this.dataservice.currency_from = this.source;
     this.dataservice.currency_to = this.target;
     this.dataservice.display = true;
      this.visible = true;
     this.showForex();
   }

  showAllData(){
    this.service.getAll().subscribe(data =>{
      this.forexProvider = data;
    });
    console.log("hello");
  }

  showForex(){
      var val = {
          currency_from : this.dataservice.currency_from,
          currency_to : this.dataservice.currency_to
      };
      console.log("test123");
      this.service.getForex(val).subscribe(data =>{
        this.forexValues = data;
        console.log(this.forexValues);
        this.listData = this.forexValues.providers;
        this.forex = this.forexValues.providers;
        console.log(this.forex);
        this.sortedData = this.forex.slice();
        console.log(this.sortedData);
        // this.forexValues.providers[0].currency_from = JSON.parse(this.forexValues.providers[0].currency_from);
        // console.log(this.forexValues.providers[0].currency_from);
        // console.log(this.forexValues.providers[0].currency_from[0].fields.buy_cash);
      });
      console.log("hellloo");

  }
}

function compare(a: number | string, b: number | string, isAsc: boolean) {
  return (a < b ? -1 : 1) * (isAsc ? 1 : -1);
}