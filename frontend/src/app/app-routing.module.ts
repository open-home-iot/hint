import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { StartComponent } from './core/start/start.component';
import { AuthSignUpComponent } from './core/auth/auth-sign-up/auth-sign-up.component';
import { PageNotFoundComponent } from './core/page-not-found/page-not-found.component';

/*
To add child routes of a parent path:
{ path: ParentPath, component: ParentComponent, children: [
  { path: ChildPath1, component: ChildComponent1 },
  { path: ChildPath2, component: ChildComponent2 }
] }
To add guards:
{ path: Path, component: Component, canActivate: [<Guard>, <Guard>, ...] }
Or for all children:
{ path: Path, component: Component, canActivateChild: [<Guard>, <Guard>, ...] }
NOTE! canDeactivate can be used to prevent navigation before saving changes.
 */

const ROUTES: Routes = [
  { path: '', component: StartComponent },
  { path: 'sign-up', component: AuthSignUpComponent },
  { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(ROUTES, { relativeLinkResolution: 'legacy' })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
