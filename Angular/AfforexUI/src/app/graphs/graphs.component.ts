import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { ChartDataSets, ChartOptions } from "chart.js";
import { Color, Label } from "ng2-charts";
import { ServiceService } from 'src/app/service.service';
import { DataService } from 'src/app/data.service';
import { HttpClient } from '@angular/common/http';
import { Chart }from 'chart.js';

@Component({
  selector: 'app-graphs',
  templateUrl: './graphs.component.html',
  styleUrls: ['./graphs.component.css']
})
export class GraphsComponent implements OnInit {
  @ViewChild('buyCard', {static: true}) private chartRef: any;
  @ViewChild('buyCash', {static: true}) private chartRef1: any;
  @ViewChild('sellCard', {static: true}) private chartRef2: any;
  @ViewChild('sellCash', {static: true}) private chartRef3: any;
  @ViewChild('LiveCurrency', {static: true}) private chartRef4: any;


  chart_buyCash :any;
  chart_buyCard :any;
  chart_sellCash :any;
  chart_sellCard :any;
  LiveCurrency :any;

  visibility :boolean = false;

  ngOnInit(): void {
    console.log(this.dataservice.display);
    if(this.dataservice.display){
      this.visibility = true;
      this.getMinMaxData();
      this.dataservice.display = false;
    }
    else{
      this.visibility = false;
      this.getLiveCurrency();
    }
  }

  constructor(private service:ServiceService, private dataservice: DataService , private http:HttpClient) { }

  graphData : any ;
  liveCurrencyData : any;  
  getLiveCurrency(){
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
                  label: "max",
                  borderColor: '#3cba9f',
                  fill: false
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
                text: 'BUY CARD',
                display: true
              }
            }
            });
    });
  }
  
  getMinMaxData(){
    var val = {
      currency_from : this.dataservice.currency_from,
      currency_to : this.dataservice.currency_to
    };
    console.log("test123");
    this.service.getMinMax(val).subscribe(data =>{
      this.graphData = data;

      this.chart_buyCard = new Chart(this.chartRef.nativeElement,{
        type: 'line',
            data: {
              labels: this.graphData.dates,
              datasets: [
                {
                  data: this.graphData.buy_card_max,
                  label: "max",
                  borderColor: '#3cba9f',
                  fill: false
                },
                {
                  data: this.graphData.buy_card_min,
                  label: "min",
                  borderColor: 'rgb(135,206,235)',
                  fill:false
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
                text: 'BUY CARD',
                display: true
              }
            }
            });

            this.chart_buyCash = new Chart(this.chartRef1.nativeElement,{
              type: 'line',
                  data: {
                    labels: this.graphData.dates,
                    datasets: [
                      {
                        data: this.graphData.buy_cash_max,
                        label: "max",
                        borderColor: '#3cba9f',
                        fill: false
                      },
                      {
                        data: this.graphData.buy_cash_min,
                        label: "min",
                        borderColor: 'rgb(135,206,235)',
                        fill:false
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
                      text: 'BUY CASH',
                      display: true
                    }
                  }
                  });

                  this.chart_sellCard = new Chart(this.chartRef2.nativeElement,{
                    type: 'line',
                        data: {
                          labels: this.graphData.dates,
                          datasets: [
                            {
                              data: this.graphData.sell_card_max,
                              label: "max",
                              borderColor: '#3cba9f',
                              fill: false
                            },
                            {
                              data: this.graphData.sell_card_min,
                              label: "min",
                              borderColor: 'rgb(135,206,235)',
                              fill:false
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
                            text: 'SELL CARD',
                            display: true
                          }
                        }
                        });
                        this.chart_sellCash = new Chart(this.chartRef3.nativeElement,{
                          type: 'line',
                              data: {
                                labels: this.graphData.dates,
                                datasets: [
                                  {
                                    data: this.graphData.sell_cash_max,
                                    label: "max",
                                    borderColor: '#3cba9f',
                                    fill: false
                                  },
                                  {
                                    data: this.graphData.sell_cash_min,
                                    label: "min",
                                    borderColor: 'rgb(135,206,235)',
                                    fill:false
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
                                  text: 'SELL CASH',
                                  display: true
                                }
                              }
                              });

    });
  }

}
