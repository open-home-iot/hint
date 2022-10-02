import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {GodmodeRoutingModule} from './godmode-routing.module';
import { GodmodeOverviewComponent } from './pages/godmode-overview/godmode-overview.component';



@NgModule({
  declarations: [
    GodmodeOverviewComponent
  ],
  imports: [
    GodmodeRoutingModule,
    CommonModule
  ]
})
export class GodmodeModule { }
