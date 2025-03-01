import { useEffect, useState } from 'react';
import { Text } from "@chakra-ui/react";
import {
  TimelineConnector,
  TimelineContent,
  TimelineDescription,
  TimelineItem,
  TimelineRoot,
  TimelineTitle,
} from "@/components/ui/timeline"

const Timeline = ({ items }) => {
    const [currentIndex, setCurrentIndex] = useState(1);

    useEffect(() => {
        function handleKeyDown(e) {
        if (e.key === " ") {
            // Move backward through items
            setCurrentIndex(0);
        } else if (e.key === "ArrowRight") {
            // Move forward through items
            setCurrentIndex((prevIndex) =>
                prevIndex === items.length - 1 ? 0 : prevIndex + 1
            );
        } else if (e.key === "l") {
            // Move forward through items
            setCurrentIndex((prevIndex) =>
                prevIndex === items.length - 1 ? 0 : prevIndex + 3
            );
        }
        }

        window.addEventListener("keydown", handleKeyDown);
        return () => window.removeEventListener("keydown", handleKeyDown);
    }, [items.length]);

    // If no items, don't render anything
    if (!items || items.length === 0) {
        return null;
    }

    const displayedItems = items.slice(0, currentIndex);

    return (
      <TimelineRoot maxW="400px" p="10px">
        {displayedItems.map(({ title, description, texts = [], icon: Icon }, index) => (
          <TimelineItem key={index}>
            <TimelineConnector>
              {/* Render the passed icon if available */}
              {Icon && <Icon />}
            </TimelineConnector>
            <TimelineContent>
              <TimelineTitle>{title}</TimelineTitle>
              <TimelineDescription>{description}</TimelineDescription>
              {texts.map((text, idx) => (
                <Text key={idx} textStyle="sm">
                  {text}
                </Text>
              ))}
            </TimelineContent>
          </TimelineItem>
        ))}
      </TimelineRoot>
    );
  };

export default Timeline;