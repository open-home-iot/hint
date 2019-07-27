import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { HumeComponent } from './hume.component';

const routes: Routes = [
  { path: 'hume', component: HumeComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HumeRoutingModule {}
