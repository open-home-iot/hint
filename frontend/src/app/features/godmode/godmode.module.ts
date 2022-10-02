import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {GodmodeRoutingModule} from './godmode-routing.module';
import { GodmodeOverviewComponent } from './pages/godmode-overview/godmode-overview.component';
import {GodmodeService} from './godmode.service';


@NgModule({
  declarations: [
    GodmodeOverviewComponent,
  ],
  imports: [
    GodmodeRoutingModule,
    CommonModule
  ],
  providers: [
    GodmodeService
  ],
})
export class GodmodeModule { }
