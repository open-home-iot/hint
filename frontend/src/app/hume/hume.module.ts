import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { HumeComponent } from './hume.component';
import { HumeListComponent } from './hume-list/hume-list.component';

import { HumeRoutingModule } from './hume-routing.module';

@NgModule({
  declarations: [
    HumeComponent,
    HumeListComponent
  ],
  imports: [
    HumeRoutingModule,
    CommonModule
  ],
  exports: [

  ]
})
export class HumeModule {}
