import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import {
  GodmodeOverviewComponent
} from './godmode-overview/godmode-overview.component';
import {GodmodeAuthGuard} from './godmode-auth.guard';

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
  { path: 'godmode', component: GodmodeOverviewComponent, canActivate: [GodmodeAuthGuard] }
];

@NgModule({
  imports: [RouterModule.forChild(ROUTES)],
  exports: [RouterModule]
})
export class GodmodeRoutingModule {}
