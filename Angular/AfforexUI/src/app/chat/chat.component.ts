import { Component, OnInit } from '@angular/core';
// import { start } from 'repl';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }


  msg: string = "";    

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
    var userHtml = '<p style="color: rgb(218, 17, 17);font-family: monospace;font-size: 17px;text-align: right;line-height: 30px;"><span>' + this.msg + "</span></p>";
    var node = document.createElement("p");
    // node.className = "botText"
    node.innerHTML = userHtml;
    this.msg = "";
    document.getElementById("chatbox")?.appendChild(node);

    document.getElementById("userInput")?.scrollIntoView({ block:"start",behavior:"smooth" });
    // let row = document.createElement('p');   
    // row.className = 'userText'; 
    // row.innerHTML = userHtml; 
    // document.querySelector('.chatbox')?.appendChild(row);

    // document
    //   .getElementById("userInput")
    //   .scrollIntoView({ block: "start", behavior: "smooth" });
    // $.get("/get", { msg: rawText }).done(function(data) {
    //   var botHtml = '<p class="botText"><span>' + data + "</span></p>";
    //   $("#chatbox").append(botHtml);
    //   document
    //     .getElementById("userInput")
    //     .scrollIntoView({ block: "start", behavior: "smooth" });
    // });
  }
}
