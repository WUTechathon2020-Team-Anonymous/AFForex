import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { ChartDataSets, ChartOptions } from "chart.js";
import { Color, Label } from "ng2-charts";
import { ServiceService } from 'src/app/service.service';
import { DataService } from 'src/app/data.service';
import { HttpClient } from '@angular/common/http';
import { Chart }from 'chart.js';

export interface Currencies{
  value:string,
  viewValue:string
}


@Component({
  selector: 'app-liverates',
  templateUrl: './liverates.component.html',
  styleUrls: ['./liverates.component.css']
})
export class LiveratesComponent implements OnInit {
  @ViewChild('LiveCurrency', {static: true}) private chartRef4: any;

  constructor(private service:ServiceService, private dataservice: DataService , private http:HttpClient) { }

  LiveCurrency :any;

  source: string = "";
  target: string = "";
  source_currencies: Currencies[] = [
    {value: 'inr', viewValue: 'Indian Rupee'},
    {value: 'usd', viewValue: 'U.S. Dollar'},
    {value: 'gbp', viewValue: 'G.B. Pound'},
    {value: 'eur', viewValue: 'Euro'},
    {value: 'aud', viewValue: 'Australian Dollar'}
  ];

  selected(){
    console.log(this.source);
    console.log(this.target);
    this.dataservice.currency_from = this.source;
    this.dataservice.currency_to = this.target;
    this.dataservice.display = true;
    this.getLiveCurrency();
  }

  ngOnInit(): void {
    this.getLiveCurrency();
  }

  liveCurrencyData : any;  
  getLiveCurrency(){
    document.getElementById("btn1")?.click;
    var val = {
      currency_from : this.dataservice.currency_from,
      currency_to : this.dataservice.currency_to
    };
    this.service.getLiveRates(val).subscribe(data =>{
      this.liveCurrencyData = data;
      console.log(this.liveCurrencyData);
      this.LiveCurrency = new Chart(this.chartRef4.nativeElement,{
        type: 'line',
            data: {
              labels: this.liveCurrencyData.dates,
              datasets: [
                {
                  data: this.liveCurrencyData.currency_value,
                  label: "Currency",
                  borderColor: '#3cba9f',
                  backgroundColor:  'rgba(2, 200, 214,0.3)',
                  fill: true
                }
              ]
            },
            options: {
              legend: {
                display: true
              },
              scales: {
                xAxes: [{
                  display: true
                }],
                yAxes: [{
                  display: true
                }],
              },
              title: {
                text: 'LIVE CURRENCY',
                display: true
              }
            }
            });
    });
  }

}
