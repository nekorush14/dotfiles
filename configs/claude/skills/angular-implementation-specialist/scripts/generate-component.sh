#!/bin/bash
# Generate Angular v21 component with test file following best practices
#
# Usage:
#   ./generate-component.sh <component-name> [output-dir]
#
# Example:
#   ./generate-component.sh user-card src/app/components
#   ./generate-component.sh button-group src/app/shared/components

set -euo pipefail

# Constants
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly DEFAULT_OUTPUT_DIR="src/app/components"

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

# Functions
print_error() {
  echo -e "${RED}ERROR: $1${NC}" >&2
}

print_success() {
  echo -e "${GREEN}SUCCESS: $1${NC}"
}

print_info() {
  echo -e "${YELLOW}INFO: $1${NC}"
}

validate_component_name() {
  local name="$1"

  # WHY: Validate component name format (lowercase with hyphens)
  if [[ ! "$name" =~ ^[a-z][a-z0-9-]*$ ]]; then
    print_error "Component name must be lowercase with hyphens (e.g., user-card, button-group)"
    return 1
  fi

  return 0
}

to_pascal_case() {
  local input="$1"
  # WHY: Convert hyphenated name to PascalCase for class name
  echo "$input" | sed -E 's/(^|-)([a-z])/\U\2/g'
}

to_camel_case() {
  local input="$1"
  # WHY: Convert hyphenated name to camelCase for variables
  echo "$input" | sed -E 's/-([a-z])/\U\1/g'
}

generate_component_file() {
  local component_name="$1"
  local output_path="$2"
  local class_name
  class_name="$(to_pascal_case "$component_name")Component"

  # WHY: Generate component file with Angular v21 best practices
  cat > "$output_path/${component_name}.component.ts" <<EOF
import { Component, ChangeDetectionStrategy, input, output, computed } from '@angular/core'
import { CommonModule } from '@angular/common'

interface ${class_name}Props {
  // TODO: Define component props
}

@Component({
  selector: 'app-${component_name}',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule],
  template: \`
    <div class="p-4">
      <h2 class="text-xl font-semibold">{{ title() }}</h2>
      <!-- TODO: Add component template -->
    </div>
  \`,
  styles: [\`
    /* TODO: Add component-specific styles if needed */
  \`],
})
export class ${class_name} {
  // WHY: Use input() function instead of @Input() decorator
  title = input<string>('Default Title')

  // WHY: Use output() function instead of @Output() decorator
  // Example: onClick = output<void>()

  // WHY: Use computed() for derived state
  // Example: isActive = computed(() => this.status() === 'active')

  // TODO: Add component logic
}
EOF

  print_success "Generated component file: $output_path/${component_name}.component.ts"
}

generate_test_file() {
  local component_name="$1"
  local output_path="$2"
  local class_name
  class_name="$(to_pascal_case "$component_name")Component"

  # WHY: Generate test file following TDD and Vitest best practices
  cat > "$output_path/${component_name}.component.spec.ts" <<EOF
import { describe, it, expect, beforeEach } from 'vitest'
import { ComponentFixture, TestBed } from '@angular/core/testing'
import { ${class_name} } from './${component_name}.component'

describe('${class_name}', () => {
  let component: ${class_name}
  let fixture: ComponentFixture<${class_name}>

  beforeEach(async () => {
    // WHY: Configure testing module with component imports
    await TestBed.configureTestingModule({
      imports: [${class_name}],
    }).compileComponents()

    fixture = TestBed.createComponent(${class_name})
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should create', () => {
    expect(component).toBeTruthy()
  })

  it('should display title', () => {
    // WHY: Set input using fixture.componentRef.setInput for signal inputs
    fixture.componentRef.setInput('title', 'Test Title')
    fixture.detectChanges()

    const compiled = fixture.nativeElement as HTMLElement
    expect(compiled.textContent).toContain('Test Title')
  })

  // TODO: Add more tests following TDD approach
  // - Test component behavior
  // - Test signal inputs and outputs
  // - Test computed signals
  // - Test user interactions
  // - Test edge cases
})
EOF

  print_success "Generated test file: $output_path/${component_name}.component.spec.ts"
}

main() {
  # Validate arguments
  if [[ $# -lt 1 ]]; then
    print_error "Component name is required"
    echo "Usage: $0 <component-name> [output-dir]"
    echo "Example: $0 user-card src/app/components"
    exit 1
  fi

  local component_name="$1"
  local output_dir="${2:-$DEFAULT_OUTPUT_DIR}"

  # Validate component name
  if ! validate_component_name "$component_name"; then
    exit 1
  fi

  # Create output directory
  local output_path="$output_dir/$component_name"
  if [[ -d "$output_path" ]]; then
    print_error "Directory already exists: $output_path"
    exit 1
  fi

  mkdir -p "$output_path"
  print_success "Created directory: $output_path"

  # Generate files
  generate_component_file "$component_name" "$output_path"
  generate_test_file "$component_name" "$output_path"

  # Summary
  echo ""
  echo "================================================"
  print_success "Component generated successfully!"
  echo "================================================"
  echo ""
  echo "Generated files:"
  echo "  - $output_path/${component_name}.component.ts"
  echo "  - $output_path/${component_name}.component.spec.ts"
  echo ""
  echo "Next steps:"
  echo "  1. Update the component template and logic"
  echo "  2. Add tests following TDD approach"
  echo "  3. Run tests: npm run test"
  echo "  4. Implement component to pass tests"
  echo "  5. Apply Tailwind CSS styling"
  echo ""
}

main "$@"
