import re

with open('frontend/src/test/setup.ts', 'w') as f:
    f.write("""import '@testing-library/jest-dom';
import { vi } from 'vitest';

const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
};

vi.stubGlobal('localStorage', localStorageMock);
""")

with open('frontend/src/test/ProxyConfigModal.test.tsx', 'r') as f:
    content = f.read()

# Make all synchronous test functions async
content = re.sub(r'it\(\'([^\']+)\', \(\) => \{', r"it('\1', async () => {", content)

# Replace getByRole with findByRole for the checkbox
content = content.replace("screen.getByRole('checkbox', { name: /enable response delay/i })", "await screen.findByRole('checkbox', { name: /enable response delay/i })")
content = content.replace("screen.getByText('Response Delay')", "await screen.findByText('Response Delay')")

with open('frontend/src/test/ProxyConfigModal.test.tsx', 'w') as f:
    f.write(content)

print("Fixed frontend tests")
