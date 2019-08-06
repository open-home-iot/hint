import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { EventOverviewComponent } from './pages/event-overview/event-overview.component';

const routes: Routes = [
  { path: 'event', component: EventOverviewComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class EventRoutingModule {}
