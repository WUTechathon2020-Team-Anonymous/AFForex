import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ForexComponent } from './forex/forex.component';

const routes: Routes = [
  {path:'forexProvider',component:ForexComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
