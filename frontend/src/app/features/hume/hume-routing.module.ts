import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { HumeOverviewComponent } from './pages/hume-overview/hume-overview.component';

const routes: Routes = [
  { path: 'hume', component: HumeOverviewComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HumeRoutingModule {}
