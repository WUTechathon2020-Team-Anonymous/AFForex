import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ForexComponent } from './forex/forex.component';
import { GraphsComponent } from './graphs/graphs.component';
import { ChatComponent } from './chat/chat.component';
import { LiveratesComponent } from './liverates/liverates.component';
import { SubscribeComponent } from './subscribe/subscribe.component';

const routes: Routes = [
  {path:'',component:ForexComponent},
  {path:'forexProvider',component:ForexComponent},
  {path:'graphs',component:LiveratesComponent},
  {path:'subscribe',component:SubscribeComponent},
  {path:'chat',component:ChatComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
