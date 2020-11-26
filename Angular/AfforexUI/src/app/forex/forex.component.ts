import { Component, OnInit } from '@angular/core';
import { ServiceService } from 'src/app/service.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-forex',
  templateUrl: './forex.component.html',
  styleUrls: ['./forex.component.css']
})
export class ForexComponent implements OnInit {

  constructor(private service:ServiceService,private http:HttpClient) { }

  forexProvider:any = []
  forexValues:any = []

  ngOnInit(): void {
    this.showAllData();
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
          target_currency : 'aud'
      };
      console.log("test123");
      this.service.getForex(val).subscribe(data =>{
        this.forexValues = data;
      });
  }
}
