import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ForexComponent } from './forex/forex.component';
import { GraphsComponent } from './graphs/graphs.component';
import { ChatComponent } from './chat/chat.component';

const routes: Routes = [
  {path:'forexProvider',component:ForexComponent},
  {path:'graphs',component:GraphsComponent},
  {path:'chat',component:ChatComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
