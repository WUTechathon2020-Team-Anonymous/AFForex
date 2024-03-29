import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs'


@Injectable({
  providedIn: 'root'
})
export class ServiceService {
readonly ApiUrl = 'http://127.0.0.1:8000';

  constructor(private http:HttpClient) { }

  getAll():Observable<any[]>{
    return this.http.get<any[]>(this.ApiUrl + '/api/');
  }

  getForex(val:any){
  	return this.http.post(this.ApiUrl + '/forex/', val);
  }

  getChat(val:any){
    return this.http.post(this.ApiUrl + '/chatbot/',val);
  }

  getMinMax(val:any){
    return this.http.post(this.ApiUrl + '/min_max_values/',val);
  }
  getLiveRates(val:any){
    return this.http.post(this.ApiUrl + '/live_rates/',val);
  }
}
