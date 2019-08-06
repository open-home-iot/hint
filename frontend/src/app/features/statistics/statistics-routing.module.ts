import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { StatisticsOverviewComponent } from './pages/statistics-overview/statistics-overview.component';

const routes: Routes = [
  { path: 'statistics', component: StatisticsOverviewComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class StatisticsRoutingModule {}
