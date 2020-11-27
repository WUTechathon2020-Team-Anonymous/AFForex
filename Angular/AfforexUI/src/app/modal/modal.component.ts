import { Component, OnInit } from '@angular/core';
import { ServiceService } from 'src/app/service.service';

import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-modal',
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.css']
})

export class ModalComponent implements OnInit {

  constructor(public dialogRef: MatDialogRef<ModalComponent>,private service: ServiceService) { }

  ngOnInit() {
  }
  email:string="";

  // When the user clicks the action button a.k.a. the logout button in the\
  // modal, show an alert and followed by the closing of the modal
  actionFunction() {
    var val = {
      email : this.email
  };
  console.log("test123");
  this.service.getEmail(val).subscribe(data =>{
    console.log(data)
  });
    this.closeModal();
  }

  // If the user clicks the cancel button a.k.a. the go back button, then\
  // just close the modal
  closeModal() {
    this.dialogRef.close();
  }

}

