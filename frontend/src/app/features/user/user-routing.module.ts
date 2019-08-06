import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { UserOverviewComponent } from './pages/user-overview/user-overview.component';

const routes: Routes = [
  { path: 'user', component: UserOverviewComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UserRoutingModule {}
