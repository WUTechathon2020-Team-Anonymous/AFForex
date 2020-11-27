import { Component, OnInit } from '@angular/core';
import { ServiceService } from 'src/app/service.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {

  constructor(private service:ServiceService,private http:HttpClient) { }

  ngOnInit(): void {
  }


  msg: string = "";
  replymsg: string = ""; 
  reply : any;

  submit($event: any){    
    console.log("Save button is clicked!", $event); 
    this.add();   
  }
  onKey(event: any) { // without type info
    console.log(event.target.value);
    console.log("CLICK");
    this.add();
  }

  add(){
    var val = {
      msg : this.msg
    };
    console.log("test123");
    this.service.getChat(val).subscribe(data =>{
      this.reply = data;
      console.log(this.reply);
    });

    var userHtml = '<p style="color: rgb(218, 17, 17);font-family: monospace;font-size: 17px;text-align: right;line-height: 30px;"><span>' + this.msg + "</span></p>";
    var node = document.createElement("p");
    // node.className = "botText"
    node.innerHTML = userHtml;
    this.msg = "";
    document.getElementById("chatbox")?.appendChild(node);
    document.getElementById("userInput")?.scrollIntoView({ block:"start",behavior:"smooth" });
    this.addreply();
  }

  addreply(){
    setTimeout(
      () =>{
      this.replymsg = this.reply.response;
      var botHtml = '<p style = "color: white;font-family: monospace;font-size: 17px;text-align: left;line-height: 30px;"><span style = "background-color: #4169e1;padding: 10px;border-radius: 2px;">' + this.replymsg + "</span></p>";
      var node = document.createElement("p");
      // node.className = "botText"
      node.innerHTML = botHtml;
      document.getElementById("chatbox")?.appendChild(node);
      console.log("output");
    },2000
    )
  }
}
