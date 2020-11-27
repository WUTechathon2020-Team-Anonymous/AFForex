import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
@Injectable()
export class DataService {
  currency_from: string = "";
  currency_to:string = "";
  display : boolean = false;
  constructor() { }
}
