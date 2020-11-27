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

    var userHtml = '<div style = "display: flex;justify-content: flex-end;align-items: center;"><span style = "display: flex;justify-content: flex-end;margin: 0.75rem;padding: 0.5rem;background-color: #ddd;border-radius: 25px;box-shadow: 0 2px 5px rgba(0, 0, 0, 0.4);word-break: break-all;">' + this.msg + '</span></div>';
    var node = document.createElement("p");
    // node.className = "botText"
    node.innerHTML = userHtml;
    this.msg = "";
    // const chatArea = document.querySelector('.chat-area');
    // chatArea.insertAdjacentHTML("beforeend", userHtml);
    document.getElementById("test2")?.appendChild(node);
    // document.getElementById("userInput")?.scrollIntoView({ block:"start",behavior:"smooth" });
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
