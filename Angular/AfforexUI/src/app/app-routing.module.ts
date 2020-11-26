import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ForexComponent } from './forex/forex.component';
import { GraphsComponent } from './graphs/graphs.component'

const routes: Routes = [
  {path:'forexProvider',component:ForexComponent},
  {path:'graphs',component:GraphsComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
