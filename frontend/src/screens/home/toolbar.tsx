import { useState } from "react";
import { Drawer, Button, Group } from "@mantine/core";
import { PiMathOperations } from "react-icons/pi"; // optional math icon

interface SymbolToolbarProps {
  onInsertSymbol?: (symbol: string) => void; // callback to send symbol to parent
}

export default function SymbolToolbar({ onInsertSymbol }: SymbolToolbarProps) {
  const [opened, setOpened] = useState(false);

  const symbols = ["+", "-", "×", "÷", "=", "%", "^", "√", "π", "(", ")", "x", "y"];

  return (
    <>
      {/* Toggle Button */}
      <Button
        onClick={() => setOpened(true)}
        variant="default"
        className="fixed top-1/2 left-2 z-50 rounded-full shadow-md"
        style={{ transform: "translateY(-50%)" }}
      >
        <PiMathOperations size={20} />
      </Button>

      {/* Drawer Toolbar */}
      <Drawer
        opened={opened}
        onClose={() => setOpened(false)}
        position="left"
        size="sm"
        title="Math Symbols"
        overlayProps={{ opacity: 0.4, blur: 2 }}
        padding="md"
        classNames={{
          body: "flex flex-wrap gap-3 justify-center",
        }}
      >
        {symbols.map((sym) => (
          <Button
            key={sym}
            variant="light"
            color="dark"
            radius="md"
            className="w-12 h-12 text-lg font-bold"
            onClick={() => {
              onInsertSymbol?.(sym);
              setOpened(false);
            }}
          >
            {sym}
          </Button>
        ))}
      </Drawer>
    </>
  );
}
