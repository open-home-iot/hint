import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';

// COMPONENTS
import { HumeFindComponent } from './hume-find/hume-find.component';
import { HumeListComponent } from './hume-list/hume-list.component';

// PAGES

// SERVICES
import { HumeService } from './hume.service';

// MODULES
import { HumeRoutingModule } from './hume-routing.module';

@NgModule({
  declarations: [
    HumeFindComponent,
    HumeListComponent
  ],
  imports: [
    HumeRoutingModule,
    CommonModule,
    ReactiveFormsModule
  ],
  exports: [
    HumeFindComponent,
    HumeListComponent
  ],
  providers: [HumeService]
})
export class HumeModule {}
