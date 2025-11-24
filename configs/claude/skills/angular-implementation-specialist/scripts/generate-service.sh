#!/bin/bash
# Generate Angular v21 service with test file following best practices
#
# Usage:
#   ./generate-service.sh <service-name> [output-dir]
#
# Example:
#   ./generate-service.sh user src/app/services
#   ./generate-service.sh auth src/app/core/services

set -euo pipefail

# Constants
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly DEFAULT_OUTPUT_DIR="src/app/services"

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

validate_service_name() {
  local name="$1"

  # WHY: Validate service name format (lowercase with hyphens)
  if [[ ! "$name" =~ ^[a-z][a-z0-9-]*$ ]]; then
    print_error "Service name must be lowercase with hyphens (e.g., user, auth-token)"
    return 1
  fi

  return 0
}

to_pascal_case() {
  local input="$1"
  # WHY: Convert hyphenated name to PascalCase for class name
  echo "$input" | sed -E 's/(^|-)([a-z])/\U\2/g'
}

generate_service_file() {
  local service_name="$1"
  local output_path="$2"
  local class_name
  class_name="$(to_pascal_case "$service_name")Service"

  # WHY: Generate service file with Angular v21 best practices
  cat > "$output_path/${service_name}.service.ts" <<EOF
import { Injectable, inject } from '@angular/core'
import { HttpClient } from '@angular/common/http'
import { Observable } from 'rxjs'

// TODO: Define interfaces for service data
interface ${class_name}Data {
  id: string
  // Add more fields
}

@Injectable({
  providedIn: 'root'
})
export class ${class_name} {
  // WHY: Use inject() function instead of constructor injection
  private readonly http = inject(HttpClient)

  // TODO: Define API endpoint
  private readonly apiUrl = '/api/${service_name}s'

  // TODO: Implement service methods
  getAll(): Observable<${class_name}Data[]> {
    return this.http.get<${class_name}Data[]>(this.apiUrl)
  }

  getById(id: string): Observable<${class_name}Data> {
    return this.http.get<${class_name}Data>(\`\${this.apiUrl}/\${id}\`)
  }

  create(data: Omit<${class_name}Data, 'id'>): Observable<${class_name}Data> {
    return this.http.post<${class_name}Data>(this.apiUrl, data)
  }

  update(id: string, data: Partial<${class_name}Data>): Observable<${class_name}Data> {
    return this.http.patch<${class_name}Data>(\`\${this.apiUrl}/\${id}\`, data)
  }

  delete(id: string): Observable<void> {
    return this.http.delete<void>(\`\${this.apiUrl}/\${id}\`)
  }
}
EOF

  print_success "Generated service file: $output_path/${service_name}.service.ts"
}

generate_test_file() {
  local service_name="$1"
  local output_path="$2"
  local class_name
  class_name="$(to_pascal_case "$service_name")Service"

  # WHY: Generate test file following TDD and Vitest best practices
  cat > "$output_path/${service_name}.service.spec.ts" <<EOF
import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { TestBed } from '@angular/core/testing'
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing'
import { ${class_name} } from './${service_name}.service'

describe('${class_name}', () => {
  let service: ${class_name}
  let httpMock: HttpTestingController

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [${class_name}],
    })

    service = TestBed.inject(${class_name})
    httpMock = TestBed.inject(HttpTestingController)
  })

  afterEach(() => {
    // WHY: Verify that no unmatched requests are outstanding
    httpMock.verify()
  })

  it('should be created', () => {
    expect(service).toBeTruthy()
  })

  it('should fetch all items', () => {
    const mockData = [
      { id: '1' },
      { id: '2' },
    ]

    service.getAll().subscribe(data => {
      expect(data).toEqual(mockData)
      expect(data.length).toBe(2)
    })

    const req = httpMock.expectOne('/api/${service_name}s')
    expect(req.request.method).toBe('GET')
    req.flush(mockData)
  })

  it('should fetch item by id', () => {
    const mockData = { id: '1' }

    service.getById('1').subscribe(data => {
      expect(data).toEqual(mockData)
    })

    const req = httpMock.expectOne('/api/${service_name}s/1')
    expect(req.request.method).toBe('GET')
    req.flush(mockData)
  })

  it('should create item', () => {
    const newData = { /* add fields */ }
    const createdData = { id: '3', ...newData }

    service.create(newData).subscribe(data => {
      expect(data).toEqual(createdData)
    })

    const req = httpMock.expectOne('/api/${service_name}s')
    expect(req.request.method).toBe('POST')
    expect(req.request.body).toEqual(newData)
    req.flush(createdData)
  })

  it('should update item', () => {
    const updateData = { /* add fields */ }
    const updatedData = { id: '1', ...updateData }

    service.update('1', updateData).subscribe(data => {
      expect(data).toEqual(updatedData)
    })

    const req = httpMock.expectOne('/api/${service_name}s/1')
    expect(req.request.method).toBe('PATCH')
    expect(req.request.body).toEqual(updateData)
    req.flush(updatedData)
  })

  it('should delete item', () => {
    service.delete('1').subscribe(() => {
      expect(true).toBe(true)
    })

    const req = httpMock.expectOne('/api/${service_name}s/1')
    expect(req.request.method).toBe('DELETE')
    req.flush(null)
  })

  it('should handle error', () => {
    service.getAll().subscribe({
      next: () => fail('should have failed with 500 error'),
      error: (error) => {
        expect(error.status).toBe(500)
      },
    })

    const req = httpMock.expectOne('/api/${service_name}s')
    req.flush('Server error', { status: 500, statusText: 'Internal Server Error' })
  })

  // TODO: Add more tests following TDD approach
  // - Test edge cases
  // - Test error handling
  // - Test data transformation
  // - Test caching if implemented
})
EOF

  print_success "Generated test file: $output_path/${service_name}.service.spec.ts"
}

main() {
  # Validate arguments
  if [[ $# -lt 1 ]]; then
    print_error "Service name is required"
    echo "Usage: $0 <service-name> [output-dir]"
    echo "Example: $0 user src/app/services"
    exit 1
  fi

  local service_name="$1"
  local output_dir="${2:-$DEFAULT_OUTPUT_DIR}"

  # Validate service name
  if ! validate_service_name "$service_name"; then
    exit 1
  fi

  # Create output directory if it doesn't exist
  if [[ ! -d "$output_dir" ]]; then
    mkdir -p "$output_dir"
    print_success "Created directory: $output_dir"
  fi

  # Check if files already exist
  if [[ -f "$output_dir/${service_name}.service.ts" ]]; then
    print_error "Service file already exists: $output_dir/${service_name}.service.ts"
    exit 1
  fi

  # Generate files
  generate_service_file "$service_name" "$output_dir"
  generate_test_file "$service_name" "$output_dir"

  # Summary
  echo ""
  echo "================================================"
  print_success "Service generated successfully!"
  echo "================================================"
  echo ""
  echo "Generated files:"
  echo "  - $output_dir/${service_name}.service.ts"
  echo "  - $output_dir/${service_name}.service.spec.ts"
  echo ""
  echo "Next steps:"
  echo "  1. Update the service interface and methods"
  echo "  2. Update tests with actual data structure"
  echo "  3. Run tests: npm run test"
  echo "  4. Implement service methods to pass tests"
  echo "  5. Add error handling and edge cases"
  echo ""
}

main "$@"
