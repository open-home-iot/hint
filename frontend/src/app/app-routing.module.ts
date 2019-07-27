import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { StartComponent } from './core/start/start.component';
import { PageNotFoundComponent } from './core/page-not-found/page-not-found.component'

const routes: Routes = [
  { path: '', component: StartComponent },
  { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
