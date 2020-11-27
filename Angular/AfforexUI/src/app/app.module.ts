import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ForexComponent } from './forex/forex.component';
import { ServiceService } from './service.service';
import { DataService } from './data.service';

import { HttpClientModule } from '@angular/common/http';
import { FormsModule,ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ChartsModule } from 'ng2-charts';
import { MatSelectModule } from '@angular/material/select';
import {MatSortModule,Sort} from '@angular/material/sort';
import { MatCellDef, MatTableDataSource,MatTableModule } from '@angular/material/table';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatIconModule} from '@angular/material/icon';

import { MatButtonModule } from '@angular/material/button';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import {MatInputModule} from '@angular/material/input';

import { DatePipe } from '@angular/common';

import { GraphsComponent } from './graphs/graphs.component';
import { ChatComponent } from './chat/chat.component';
import { from } from 'rxjs';
import { LiveratesComponent } from './liverates/liverates.component';
import { ModalComponent } from './modal/modal.component';
import { SubscribeComponent } from './subscribe/subscribe.component';




@NgModule({
  declarations: [
    AppComponent,
    ForexComponent,
    GraphsComponent,
    ChatComponent,
    LiveratesComponent,
    ModalComponent,
    SubscribeComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    MatSelectModule,
    ChartsModule,
    MatSortModule,
    MatTableModule,
    MatFormFieldModule,
    MatIconModule,
    MatDialogModule,
    MatButtonModule,
    MatInputModule
  ],
  providers: [ServiceService,DataService,DatePipe],
  bootstrap: [AppComponent],
  entryComponents: [ModalComponent]

})
export class AppModule { }
