import { Component, OnInit } from '@angular/core';
import { ChartDataSets, ChartOptions } from "chart.js";
import { Color, Label } from "ng2-charts";

@Component({
  selector: 'app-graphs',
  templateUrl: './graphs.component.html',
  styleUrls: ['./graphs.component.css']
})
export class GraphsComponent implements OnInit {
  ngOnInit(): void {
  }
  lineChartData: ChartDataSets[] = [
    { data: [85, 88, 78.34, 75, 77, 75], label: 'USD prices' },
  ];

  lineChartLabels: Label[] = ['20/11', '21/11', '22/11', '23/11', '24/11', '25/11'];

  lineChartOptions = {
    responsive: true,
  };

  lineChartColors: Color[] = [
    {
      borderColor: 'black',
      backgroundColor: 'rgba(135,206,235,0.4)',
    },
  ];

  lineChartLegend = true;
  lineChartPlugins = [];
  lineChartType = 'line';
}
