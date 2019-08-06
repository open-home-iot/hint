import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { HomeOverviewComponent } from './pages/home-overview/home-overview.component';

const routes: Routes = [
  { path: 'home', component: HomeOverviewComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HomeRoutingModule {}
